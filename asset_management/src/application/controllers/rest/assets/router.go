package assets

import (
	"github.com/gin-gonic/gin"
)

func AssetRouter(rg *gin.RouterGroup) {
	rg.POST("", createAsset)
	rg.GET("", findAssets)
	rg.GET(":id", getAsset)
	rg.PUT(":id", updateAsset)
	rg.DELETE(":id", deleteAsset)
}
