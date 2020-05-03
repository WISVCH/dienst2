package handlers

import (
	"fmt"
	"github.com/WISVCH/member-registration/entities"
	"github.com/gin-gonic/gin"
	"net/http"
)

type formParams struct {
	FirstName string `form:"fname" binding:"required"`
	LastName  string `form:"lastname" binding:"required"`
	BirthDate string `form:"birthdate" binding:"required"`
}

type MemberInformation struct {
	formParams formParams
	hasPayed   bool
	IsApproved bool
}

func MemberFormHandler(i entities.HandlerInteractor) func(c *gin.Context) {
	return func(c *gin.Context) {
		var form entities.FormEntity
		if err := c.ShouldBind(&form); err != nil {
			fmt.Println(err.Error())
			c.String(http.StatusBadRequest, "Data received does not match expected form")
			return
		}
		if err, message := handleRegistration(&form, i); err != nil {
			c.HTML(http.StatusInternalServerError, "error.tmpl", gin.H{"errorMessage": message})
			return
		}

		c.IndentedJSON(http.StatusOK, gin.H{"formdata": form})
	}
}

func MemberFormRender(i entities.HandlerInteractor) func(c *gin.Context) {
	return func(c *gin.Context) {
		c.HTML(http.StatusOK, "memberForm.tmpl", gin.H{})
	}
}

func handleRegistration(f *entities.FormEntity, i entities.HandlerInteractor) (error, string) {
	memberEntry := *f
	fmt.Println(memberEntry)
	if err := i.DB.AddFormEntry(memberEntry); err != nil {
		return err, "Unable to insert entry into database"
	}
	return nil, ""
}
