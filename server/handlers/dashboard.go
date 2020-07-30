package handlers

import (
	"fmt"
	"github.com/WISVCH/member-registration/config"
	"github.com/WISVCH/member-registration/entities"
	"github.com/gin-gonic/gin"
	"net/http"
)

func Formlist(i entities.HandlerInteractor) func(c *gin.Context) {
	return func(c *gin.Context) {
		var forms, err = i.DB.ListForms()
		if err != nil{
			fmt.Print(err)
		}

		c.IndentedJSON(http.StatusOK, gin.H{"formdata": forms})
	}
}

func SubmitForm(i entities.HandlerInteractor, config config.Config) func(c *gin.Context){
	return func(c *gin.Context) {
		http.Post(config.DienstApiUrl) // TODO
		var forms, err = i.DB.ListForms()
		if err != nil{
			fmt.Print(err)
		}

		c.IndentedJSON(http.StatusOK, gin.H{"formdata": forms})
	}
}
