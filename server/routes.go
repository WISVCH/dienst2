package server

import (
	"github.com/WISVCH/member-registration/entities"
	"github.com/WISVCH/member-registration/server/handlers"
	"github.com/gin-gonic/gin"
	"github.com/WISVCH/member-registration/server/utils/auth"
)

func registerPublicRoutes(router *gin.RouterGroup, i entities.HandlerInteractor) {
	i.RegisterDefaultMiddleware(router)
	router.GET("/form", handlers.MemberFormRender(i))
}

func registerAdminRoutes(router *gin.RouterGroup, i entities.HandlerInteractor) {
	i.RegisterDefaultMiddleware(router)
	router.GET("/formlist", handlers.Formlist(i))
	//router.Use(auth.ConnectMiddleware())
}

func registerApiRoutes(router * gin.RouterGroup, i entities.HandlerInteractor){
	i.RegisterDefaultMiddleware(router)
	router.POST("/form", handlers.MemberFormHandler(i))
}

func registerAuthRoutes(router *gin.RouterGroup, i entities.HandlerInteractor){
	i.RegisterDefaultMiddleware(router)
	router.GET("/connect/callback", auth.CallbackController())
	router.GET("/connect/login", auth.LoginController())
}