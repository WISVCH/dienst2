package server

import (
	"github.com/WISVCH/member-registration/entities"
	"github.com/WISVCH/member-registration/server/handlers"
	"github.com/gin-gonic/gin"
)

func registerPublicRoutes(router *gin.RouterGroup, i entities.HandlerInteractor) {
	i.RegisterDefaultMiddleware(router)
	//router.GET("/status", handlers.Status(i))
	router.GET("/form", handlers.MemberFormRender(i))
	//router.POST("/admin/auth", handlers.AuthenticateUser(i, true))
}

func registerAdminRoutes(router *gin.RouterGroup, i entities.HandlerInteractor) {
	i.RegisterDefaultMiddleware(router)
}

func registerApiRoutes(router * gin.RouterGroup, i entities.HandlerInteractor){
	i.RegisterDefaultMiddleware(router)
	router.POST("/form", handlers.MemberFormHandler(i))
}