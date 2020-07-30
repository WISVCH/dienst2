package server

import (
	"github.com/WISVCH/member-registration/entities"
	"github.com/WISVCH/member-registration/server/handlers"
	"github.com/WISVCH/member-registration/server/utils/auth"
	"github.com/gin-gonic/gin"
)

func registerPublicRoutes(router *gin.RouterGroup, i entities.HandlerInteractor) {
	i.RegisterDefaultMiddleware(router)
	router.GET("/form", handlers.MemberFormRender(i))
}

func registerAdminRoutes(router *gin.RouterGroup, i entities.HandlerInteractor) {
	i.RegisterDefaultMiddleware(router)
	router.Use(auth.ConnectMiddleware())
	router.GET("/formlist", handlers.Formlist(i))
}

func registerApiRoutes(router *gin.RouterGroup, i entities.HandlerInteractor) {
	i.RegisterDefaultMiddleware(router)
	router.POST("/form", handlers.MemberFormHandler(i))
}

func registerAuthRoutes(router *gin.RouterGroup, i entities.HandlerInteractor) {
	i.RegisterDefaultMiddleware(router)
	router.GET("/connect/callback", auth.CallbackController(i))
	router.GET("/connect/login", auth.LoginController())
	router.GET("/connect/logout", auth.LogOutController(i))
}
