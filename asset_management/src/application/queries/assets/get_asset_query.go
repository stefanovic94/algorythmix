package assets

import (
	Entities "asset_management/src/domain/entities"
	AssetRepository "asset_management/src/infrastructure/adapters"
	logger "asset_management/src/libs/logging"
)

func GetAssetQuery(id string) *Entities.Asset {
	log := logger.GetLogger()

	obj, err := AssetRepository.GetAsset(id)
	if err != nil {
		log.Error().Err(err).Str("asset", id).Msg("error getting asset")
		// TODO improve error handling
		return nil
	}

	return obj
}
