package handlers

import (
	"bytes"
	"fmt"
	"github.com/WISVCH/member-registration/config"
	"github.com/WISVCH/member-registration/entities"
	"github.com/gin-gonic/gin"
	"io/ioutil"
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
		var jsonStr = `{
    "revision_comment": "tset",
    "member": {
        "person": null,
        "date_from": null,
        "date_to": null,
        "date_paid": null,
        "amount_paid": null,
        "merit_date_from": null,
        "merit_invitations": false,
        "honorary_date_from": null
    },
    "student": {
        "person": "Julian",
        "enrolled": false,
        "study": "dafa",
        "first_year": true,
        "student_number": "12312",
        "emergency_name": "",
        "emergency_phone": "",
        "yearbook_permission": false,
        "date_verified": null
    },
    "alumnus": {
        "person": null,
        "study": "",
        "study_first_year": null,
        "study_last_year": null,
        "study_research_group": "",
        "study_paper": "",
        "study_professor": "",
        "work_company": "",
        "work_position": "",
        "work_sector": "",
        "contact_method": null
    },
    "employee": {
        "person": null,
        "faculty": "",
        "department": "",
        "function": "",
        "phone_internal": ""
    },
    "street_name": "adfdfdafad",
    "house_number": "2",
    "address_2": "",
    "address_3": "",
    "postcode": "2811WD",
    "city": "Reeuwijk",
    "country": "NL",
    "email": "jmcvandijk@student.tudelft.nl",
    "phone_fixed": "",
    "machazine": false,
    "board_invites": false,
    "constitution_card": false,
    "christmas_card": false,
    "yearbook": false,
    "titles": "d",
    "initials": "a",
    "firstname": "d",
    "preposition": "d",
    "surname": "d",
    "postfix_titles": "d",
    "phone_mobile": "d",
    "gender": "male",
    "birthdate": "09/04/1999",
    "deceased": false,
    "mail_announcements": false,
    "mail_company": false,
    "mail_education": false,
    "ldap_username": "juliand",
    "email_forward": false,
    "netid": "jmcvdijk",
    "linkedin_id": "",
    "facebook_id": ""
}`
		req, er := http.NewRequest("POST", config.DienstApiUrl, bytes.NewBuffer([]byte(jsonStr)))
		if er != nil{
			fmt.Print(er)
		}
		req.Header.Set("Authorization", fmt.Sprintf("Token %s", config.DienstToken))
		req.Header.Set("Content-Type", "application/json")
		print(req.Header.Get("Authorization"))

		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			panic(err)
		}
		defer resp.Body.Close()

		body, _ := ioutil.ReadAll(resp.Body)

		c.IndentedJSON(http.StatusOK, gin.H{"status": resp.Status, "body": string(body), "request": jsonStr})
	}
}
