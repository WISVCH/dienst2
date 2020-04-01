package main

import (
	"github.com/gin-gonic/gin"
	"./server"
)

func main() {
	r := gin.Default()
	r.LoadHTMLGlob("./templates/*")

	r.POST("/form", server.MemberFormHandler)
	r.GET("/form", server.MemberFormRender)

	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
