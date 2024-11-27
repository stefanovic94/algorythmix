package adapters

import (
	"asset_management/src/configs"
	"asset_management/src/domain/entities"
	"context"
	"go.mongodb.org/mongo-driver/bson"
)

func GetAsset(id string) entities.Asset {
	collection := configs.Services.Mongodb.Database("AssetManagement").Collection("Assets")

	obj := entities.Asset{}

	err := collection.FindOne(context.TODO(), bson.M{"_id": id}).Decode(&obj)
	if err != nil {
		// TODO determine error handling strategy here
		panic(err)
	}

	return obj
}

func CreateAsset(obj entities.Asset) entities.Asset {
	collection := configs.Services.Mongodb.Database("AssetManagement").Collection("Assets")

	_, err := collection.InsertOne(context.TODO(), obj)
	if err != nil {
		// TODO determine error handling strategy here
		panic(err)
	}

	return obj
}

func FindAssets(ctx context.Context, sort string, limit int) []entities.Asset {
	// collection := configs.Services.Mongodb.Database("AssetManagement").Collection("Assets")
	return []entities.Asset{}
}
