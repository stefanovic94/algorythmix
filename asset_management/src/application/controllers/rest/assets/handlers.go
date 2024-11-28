package assets

import (
	AssetCommands "asset_management/src/application/commands/assets"
	AssetQueries "asset_management/src/application/queries/assets"
	Entities "asset_management/src/domain/entities"
	"github.com/gin-gonic/gin"
	"github.com/jinzhu/copier"
	"net/http"
	"strconv"
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

	assetCreated := make(chan Entities.Asset)

	go AssetCommands.CreateAssetCommand(assetCreated, obj.Symbol)

	msg := <-assetCreated

	var responseData AssetResponse
	if err := copier.Copy(&responseData, &msg); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"status": "could not convert internal data structure to response data structure",
		})
		return
	}

	c.JSON(http.StatusCreated, responseData)
}

func findAssets(c *gin.Context) {
	industry := c.DefaultQuery("industry", "")
	sort := c.DefaultQuery("sort", "+symbol")
	limitParam := c.DefaultQuery("limit", "0")

	if limitParam != "" {
		limit, err := strconv.Atoi(limitParam)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"status": "invalid limit parameter",
			})
			return
		}
		print(limit)
	}

	objs := AssetQueries.FindAssetsQuery(industry, sort, 0)

	var response []AssetResponse
	for _, obj := range objs {
		var res AssetResponse
		if err := copier.Copy(&res, &obj); err != nil {
			continue
		}
		response = append(response, res)
	}

	if response == nil {
		response = []AssetResponse{}
	}

	c.JSON(http.StatusOK, gin.H{
		"items": response,
	})
}

func getAsset(c *gin.Context) {
	id := c.Param("id")

	obj := AssetQueries.GetAssetQuery(id)
	if obj == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"status": "asset not found",
		})
		return
	}

	var responseData AssetResponse
	if err := copier.Copy(&responseData, &obj); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"status": "could not convert internal data structure to response data structure",
		})
		return
	}

	c.JSON(http.StatusOK, responseData)
}

func updateAsset(c *gin.Context) {
	// id := c.Param("id")

	// TODO

	c.JSON(http.StatusOK, gin.H{
		"status": "ok",
	})
}

// deleteAsset handles the HTTP DELETE request to remove an asset by its ID.
//
// The function extracts the asset ID from the URL parameters, initiates an asynchronous
// deletion operation, and immediately responds with a HTTP 204 (No Content) status.
//
// Parameters:
//   - c (*gin.Context): The Gin context instance, which holds the request details and
//     response writer.
//
// Flow:
//  1. The asset ID is extracted from the URL parameters using `c.Param("id")`.
//  2. A channel `assetDeleted` is created to receive the deletion status.
//  3. The `DeleteAssetCommand` function is called in a separate goroutine and passed
//     the `assetDeleted` channel and the asset ID.
//  4. The API response is immediately sent with an HTTP status code 204.
//
// Note:
//   - To handle potential errors when looking up or deleting non-existing assets,
//     further enhancements are required, such as implementing an asset lookup
//     before the deletion command.
//
// Example usage:
//
//	DELETE /assets/:id
//
// Response:
//
//	HTTP/1.1 204 No Content
func deleteAsset(c *gin.Context) {
	id := c.Param("id")

	obj := AssetQueries.GetAssetQuery(id)
	if obj == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"status": "asset not found",
		})
		return
	}

	assetDeleted := make(chan string)

	go AssetCommands.DeleteAssetCommand(assetDeleted, id)

	c.JSON(http.StatusNoContent, gin.H{})
}
