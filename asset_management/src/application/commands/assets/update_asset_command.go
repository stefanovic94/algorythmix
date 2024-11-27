package assets

import (
	"asset_management/src/domain/entities"
	// "asset_management/src/domain/events"
	"asset_management/src/libs/logging"
)

func UpdateAssetCommand(c chan<- entities.Asset, obj entities.Asset) {
	log := logger.GetLogger()

	log.Info().Str("id", obj.ID).Msg("updating asset...")

	// TODO update asset

	// go events.AssetUpdated(c, obj)

	log.Info().Str("id", obj.ID).Msg("asset updated...")
}
