package assets

import (
	"asset_management/src/domain/entities"
	AssetRepository "asset_management/src/infrastructure/adapters"
)

func FindAssetsQuery(params AssetRepository.FindAssetsQueryParams) []entities.Asset {
	return AssetRepository.FindAssets(params)
}
