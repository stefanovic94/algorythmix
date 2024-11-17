package main

import (
	"github.com/gin-gonic/gin"
	"log"

	"net/http"
)

func main() {
	router := gin.Default()

	router.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status": "ok",
		})
	})

	log.Fatal(router.Run(":8000"))
}
