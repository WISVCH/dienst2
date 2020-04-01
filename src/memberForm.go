package main

import (
	"fmt"
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

func MemberFormHandler(c *gin.Context) {
	var form formParams
	if err := c.ShouldBind(&form); err != nil {
		fmt.Println(err.Error())
		c.String(http.StatusBadRequest, "Data received does not match expected form")
		return
	}
	if err, message := form.handleRegistration(); err != nil {
		c.HTML(http.StatusInternalServerError, "error.tmpl", gin.H{"errorMessage": message})
		return
	}

	c.IndentedJSON(http.StatusOK, gin.H{"formdata": form})
}

func MemberFormRender(c *gin.Context) {
	c.HTML(http.StatusOK, "memberForm.tmpl", gin.H{})
}

func (f *formParams) handleRegistration() (error, string) {
	// TODO: Add database to add registration to
	memberEntry := MemberInformation{*f, false, false}
	fmt.Println(memberEntry)
	return nil, ""
}
