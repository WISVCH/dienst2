package server

import (
	"fmt"
	"strconv"
	"github.com/WISVCH/member-registration/config"
	"github.com/WISVCH/member-registration/entities"
	dbRepo "github.com/WISVCH/member-registration/server/data/repositories/db"
	"github.com/WISVCH/member-registration/server/middleware"
	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
	log "github.com/sirupsen/logrus"
)

type GinServer struct {
	port   int
	Router *gin.Engine
}

func Start(c config.Config) error {
	fmt.Println("Starting server")
	connStr := c.DatabaseConnectionString()
	dbConn, err := sqlx.Open("postgres", connStr)
	if err != nil {
		panic(err)
	}
	db := dbRepo.InitDBRepo(dbConn)
	handlerInteractor := entities.HandlerInteractor{
		DB:                        db,
		RegisterDefaultMiddleware: getDefaultMiddleware(),
	}
	initLogger(c)
	server := newServer(c.ServerPort, c.IsDevMode, handlerInteractor)
	return server.Start()
}

func newServer(port int, debug bool, hi entities.HandlerInteractor) GinServer {
	server := GinServer{}
	server.port = port
	server.Router = gin.New()
	if debug {
		gin.SetMode(gin.DebugMode)
	} else {
		gin.SetMode(gin.ReleaseMode)
	}

	r := server.Router
	r.LoadHTMLGlob("./templates/*")


	hi.RegisterDefaultMiddleware(r)
	registerPublicRoutes(r.Group(""), hi)
	registerAdminRoutes(r.Group("/admin"), hi)
	registerApiRoutes(r.Group("/api"), hi)

	return server
}

func initLogger(c config.Config) {
	if !c.IsDevMode { // Is production mode, so use JSON
		log.SetFormatter(&log.JSONFormatter{})
		log.SetLevel(log.InfoLevel)
	} else {
		log.SetLevel(log.TraceLevel) // Lowest level in Logrus
	}
}

func getDefaultMiddleware() func(router entities.MiddlewareRegisterable) {
	return func(router entities.MiddlewareRegisterable) {
		router.Use(gin.Recovery())
		router.Use(middleware.GinLogger())
	}
}

func (s GinServer) Start() error {
	return s.Router.Run(":" + strconv.Itoa(s.port))
}
