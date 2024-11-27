package assets

import (
	"asset_management/src/domain/entities"
	"asset_management/src/infrastructure/adapters"
)

func GetAssetQuery(id string) entities.Asset {
	return adapters.GetAsset(id)
}
