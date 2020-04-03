package entities

import "github.com/gin-gonic/gin"

type DBRepo interface {
// Misc helpers
GetContext(c *gin.Context) (Context, error)

}

type MiddlewareRegisterable interface {
Use(middleware ...gin.HandlerFunc) gin.IRoutes
}

type HandlerInteractor struct {
ApplicationUrl            string
DB                        DBRepo
RegisterDefaultMiddleware func(router MiddlewareRegisterable)
}

type Context struct {
	Ldap_groups []string
	Preferred_username []string
}