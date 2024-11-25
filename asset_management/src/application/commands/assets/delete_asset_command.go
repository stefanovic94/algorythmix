package assets

import (
	"asset_management/src/domain/entities"
	// "asset_management/src/domain/events"
	"asset_management/src/libs/logging"
)

func DeleteAssetCommand(c chan<- entities.Asset, obj entities.Asset) {
	log := logger.GetLogger()

	log.Info().Str("id", obj.ID).Msg("deleting asset...")

	// TODO delete asset

	// go events.AssetDeleted(c, obj)

	log.Info().Str("id", obj.ID).Msg("asset deleted...")
}
