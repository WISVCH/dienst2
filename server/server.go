package server

import (
	"fmt"
	"github.com/WISVCH/member-registration/config"
	"github.com/WISVCH/member-registration/entities"
	dbRepo "github.com/WISVCH/member-registration/server/data/repositories/db"
	"github.com/WISVCH/member-registration/server/middleware"
	"github.com/WISVCH/member-registration/server/utils/auth"
	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
	"strconv"
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
		ApplicationUrl: c.Domain,
	}
	auth.Connect(c.ConnectUrl, c.ConnectClientId, c.ClientSecret, c.RedirectUrl, c.AllowedLdap)
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
	r.LoadHTMLGlob("./resources/templates/*")

	hi.RegisterDefaultMiddleware(r)
	registerPublicRoutes(r.Group(""), hi)
	registerAdminRoutes(r.Group("/admin"), hi)
	registerApiRoutes(r.Group("/api"), hi)
	registerAuthRoutes(r.Group("/auth"), hi)

	return server
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
