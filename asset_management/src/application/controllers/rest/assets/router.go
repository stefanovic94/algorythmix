package assets

import (
	"asset_management/src/application/commands/assets"
	"asset_management/src/domain/entities"

	"github.com/gin-gonic/gin"
	"log"
	"net/http"
)

func AssetRouter(rg *gin.RouterGroup) {
	rg.POST("", func(c *gin.Context) {
		var obj CreateAsset

		err := c.Bind(&obj)

		if err != nil {
			log.Printf("Error: %s", err)
			c.JSON(http.StatusBadRequest, gin.H{
				"status": "error",
			})
			return
		}

		assets.CreateAssetCommand(make(chan entities.Asset), obj.symbol)

		c.JSON(http.StatusCreated, gin.H{
			"status": "asset created",
		})
	})

	rg.GET("", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status": "ok",
		})
	})

	rg.GET(":id", func(c *gin.Context) {
		id := c.Param("id")

		log.Printf("ID: %s", id)

		c.JSON(http.StatusOK, gin.H{
			"status": "ok",
		})
	})

	rg.PUT(":id", func(c *gin.Context) {
		id := c.Param("id")

		log.Printf("ID: %s", id)

		c.JSON(http.StatusOK, gin.H{
			"status": "ok",
		})
	})

	rg.DELETE(":id", func(c *gin.Context) {
		id := c.Param("id")

		log.Printf("ID: %s", id)

		c.JSON(http.StatusOK, gin.H{
			"status": "ok",
		})
	})

}
