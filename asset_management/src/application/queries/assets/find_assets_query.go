package assets

import (
	"asset_management/src/domain/entities"
	AssetRepository "asset_management/src/infrastructure/adapters"
	logger "asset_management/src/libs/logging"
)

func FindAssetsQuery(params AssetRepository.FindAssetsQueryParams) []entities.Asset {
	log := logger.GetLogger()

	objs, err := AssetRepository.FindAssets(params)
	if err != nil {
		log.Error().Err(err).Msg("error finding assets")
		// TODO improve error handling
		return nil
	}

	return objs
}
