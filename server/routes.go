package server

import (
"github.com/WISVCH/member-registration/entities"
"github.com/WISVCH/member-registration/server/handlers"
"github.com/WISVCH/member-registration/server/middleware"
"github.com/gin-gonic/gin"
)

func registerPublicRoutes(router *gin.RouterGroup, i entities.HandlerInteractor) {
	i.RegisterDefaultMiddleware(router)
	router.GET("/status", handlers.Status(i))
	router.POST("/admin/auth", handlers.AuthenticateUser(i, true))
}

func registerAdminRoutes(router *gin.RouterGroup, i entities.HandlerInteractor) {
	i.RegisterDefaultMiddleware(router)
	router.Use(middleware.JWTAuthMiddleware(middleware.AdminAuthChecker(i)))
	router.GET("/votes-export", handlers.GetVotesExport(i))
