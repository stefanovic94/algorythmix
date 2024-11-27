package adapters

import (
	"asset_management/src/configs"
	"asset_management/src/domain/entities"
	"asset_management/src/infrastructure/dtos"
	"context"
	"errors"
	"github.com/jinzhu/copier"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"time"
)

type FindAssetsQueryParams struct {
	Industry string
	SortBy   string
	Limit    int
}

func GetAsset(id string) (*entities.Asset, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	collection := configs.Services.Mongodb.Database("AssetManagement").Collection("Assets")

	dto := dtos.AssetDto{}

	err := collection.FindOne(ctx, bson.M{"_id": id}).Decode(&dto)
	if errors.Is(err, mongo.ErrNoDocuments) {
		return nil, err
	} else if err != nil {
		// TODO determine error handling strategy here
		return nil, err
	}

	var obj entities.Asset
	if err := copier.Copy(&obj, &dto); err != nil {
		// TODO determine error handling strategy here
		return nil, err
	}

	return &obj, nil
}

func CreateAsset(obj entities.Asset) (*entities.Asset, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	collection := configs.Services.Mongodb.Database("AssetManagement").Collection("Assets")

	dto := dtos.AssetDto{}

	if err := copier.Copy(&dto, &obj); err != nil {
		// TODO determine error handling strategy here
		return nil, err
	}

	if _, err := collection.InsertOne(ctx, dto); err != nil {
		// TODO determine error handling strategy here
		return nil, err
	}

	return &obj, nil
}

func FindAssets(params FindAssetsQueryParams) ([]entities.Asset, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	collection := configs.Services.Mongodb.Database("AssetManagement").Collection("Assets")

	var objs []dtos.AssetDto

	cursor, err := collection.Find(ctx, bson.M{})
	if err != nil {
		// TODO determine error handling strategy here
		return nil, err
	}
	defer cursor.Close(ctx)

	err = cursor.All(ctx, &objs)
	if err != nil {
		// TODO determine error handling strategy here
		return nil, err
	}

	var assets []entities.Asset

	for _, obj := range objs {
		var entity entities.Asset
		if err := copier.Copy(&entity, &obj); err != nil {
			// TODO determine error handling strategy here
			return nil, err
		}
		assets = append(assets, entity)
	}

	return assets, nil
}

func DeleteAsset(id string) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	collection := configs.Services.Mongodb.Database("AssetManagement").Collection("Assets")

	if _, err := collection.DeleteOne(ctx, bson.M{"_id": id}); err != nil {
		// TODO determine error handling strategy here
		return err
	}

	return nil
}
