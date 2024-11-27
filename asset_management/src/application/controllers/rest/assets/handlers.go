package assets

import (
	assetCommands "asset_management/src/application/commands/assets"
	assetQueries "asset_management/src/application/queries/assets"
	"asset_management/src/domain/entities"
	"github.com/gin-gonic/gin"
	"net/http"
)

func createAsset(c *gin.Context) {
	var obj CreateAsset

	err := c.BindJSON(&obj)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"status": "invalid request body",
		})
		return
	}

	assetCreated := make(chan entities.Asset)

	assetCommands.CreateAssetCommand(assetCreated, obj.Symbol)

	msg := <-assetCreated

	c.JSON(http.StatusCreated, gin.H{
		"id":     msg.ID,
		"symbol": msg.Symbol,
	})
}

func findAssets(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "ok",
	})
}

func getAsset(c *gin.Context) {
	id := c.Param("id")

	obj := assetQueries.GetAssetQuery(id)

	c.JSON(http.StatusOK, gin.H{
		"_id":        obj.ID,
		"symbol":     obj.Symbol,
		"short_name": obj.ShortName,
	})
}

func updateAsset(c *gin.Context) {
	// id := c.Param("id")

	c.JSON(http.StatusOK, gin.H{
		"status": "ok",
	})
}

func deleteAsset(c *gin.Context) {
	// id := c.Param("id")

	c.JSON(http.StatusNoContent, gin.H{})
}
