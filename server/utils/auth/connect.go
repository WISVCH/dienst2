package auth

import (
	"context"
	"fmt"
	"github.com/WISVCH/member-registration/entities"
	"github.com/coreos/go-oidc"
	"github.com/gin-gonic/gin"
	log "github.com/sirupsen/logrus"
	"golang.org/x/oauth2"
	"net/http"
	"strings"
)

var connectConfig oauth2.Config
var verifier *oidc.IDTokenVerifier
var allowedGroup string

func Connect(URL, clientID, clientSecret, redirectURL, group string) {
	ctx := context.Background()

	allowedGroup = group

	var err error
	provider, err := oidc.NewProvider(ctx, URL)
	if err != nil {
		log.Fatalf("unable to create new authentication provider, error: %s", err)
	}

	verifier = provider.Verifier(&oidc.Config{ClientID: clientID})

	// Configure an OpenID Connect aware OAuth2 client.
	connectConfig = oauth2.Config{
		ClientID:     clientID,
		ClientSecret: clientSecret,
		RedirectURL:  redirectURL,

		// Discovery returns the OAuth2 endpoints.
		Endpoint: provider.Endpoint(),

		// "openid" is a required scope for OpenID Connect flows.
		Scopes: []string{oidc.ScopeOpenID, "ldap"},
	}
}

func ConnectMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader, err := c.Cookie("authorization")
		if err == nil {
			auth := strings.Split(authHeader, " ")

			if len(auth) != 2 || auth[0] != "Bearer" {
				log.Errorf("Wrong authorization header, was %s", authHeader)
				c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
					"errorMessage": "Incorrect authorization header",
				})
				return
			}

			if checkAuth(auth[1]) {
				c.Next()
				return
			}
		}

		c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
			"errorMessage": "Missing authentication",
		})
	}
}

func LoginController() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Redirect(http.StatusFound, connectConfig.AuthCodeURL("login"))
	}
}

func LogOutController(i entities.HandlerInteractor) gin.HandlerFunc {
	return func(c *gin.Context) {
		c.SetCookie("authorization", "", 0, "/", i.ApplicationUrl, false, true)
	}
}

func CallbackController(i entities.HandlerInteractor) gin.HandlerFunc {
	return func(c *gin.Context) {
		token, err := connectConfig.Exchange(context.TODO(), c.Query("code"))
		if err != nil {
			log.Errorf("unable to exchange token \"%s\", error: %s", c.Query("code"), err)
			return
		}

		rawIDToken, ok := token.Extra("id_token").(string)
		if !ok {
			log.Errorf("unable to get id_token from login")
			return
		}

		if checkAuth(rawIDToken) {
			c.SetCookie("authorization", fmt.Sprintf("Bearer %s", rawIDToken),60*60*24,"/", i.ApplicationUrl,false, true)
			c.JSON(http.StatusOK, gin.H{
				"token": rawIDToken,
			})
		} else {
			c.AbortWithStatus(http.StatusUnauthorized)
		}
	}
}

func checkAuth(rawIDToken string) bool {
	idToken, err := verifier.Verify(context.TODO(), rawIDToken)
	if err != nil {
		log.Errorf("unable to verify id_token, error: %s", err)
		return false
	}

	var claims struct {
		Groups []string `json:"ldap_groups"`
	}
	if err := idToken.Claims(&claims); err != nil {
		log.Errorf("unable to read ldap_groups from id_token, error: %s", err)
		return false
	}

	for _, group := range claims.Groups {
		if group == allowedGroup {
			return true
		}
	}
	return false
}
