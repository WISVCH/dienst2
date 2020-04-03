package middleware

import (
	"fmt"
	"github.com/gin-gonic/gin"
	log "github.com/sirupsen/logrus"
	"math"
	"time"
)

const (
	MaxRequestTimeBeforeLoggingError = 1000
)

func GinLogger() gin.HandlerFunc {
	var timeFormat = "02/Jan/2006:15:04:05 -0700"
	return func(c *gin.Context) {
		method := c.Request.Method
		path := c.Request.URL.Path
		reqEmail := c.Request.Header.Get("X-Auth-Email")
		start := time.Now()
		c.Next() // Start handling request
		stop := time.Since(start)
		latency := int(math.Ceil(float64(stop.Nanoseconds()) / 1000000.0))
		status := c.Writer.Status()

		entry := log.WithFields(log.Fields{
			"status_code":  status,
			"latency":      latency,
			"client_ip":    c.ClientIP(),
			"x-auth-email": reqEmail,
			"method":       method,
			"path":         path,
			"data_length":  c.Writer.Size(),
			"user_agent":   c.Request.UserAgent(),
			"timestamp":    time.Now().Format(timeFormat),
		})

		if len(c.Errors) > 0 {
			entry.Error(c.Errors.ByType(gin.ErrorTypePrivate).String())
		} else {
			msg := fmt.Sprintf("%d response sent for %s %s by %s", status, method, path, reqEmail)
			if status >= 500 {
				entry.Error(msg)
			} else if latency > MaxRequestTimeBeforeLoggingError {
				requestLatencyError := fmt.Sprintf("response sent, but marked as error due to request latency being too long, the latency of %dms exceeded the threshold of %dms", latency, MaxRequestTimeBeforeLoggingError)
				entry.Error(requestLatencyError)
			} else if status >= 400 {
				entry.Warn(msg)
			} else {
				entry.Info(msg)
			}
		}
	}
}
