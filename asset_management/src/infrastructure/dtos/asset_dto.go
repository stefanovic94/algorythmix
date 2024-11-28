package dtos

type AssetDto struct {
	ID                  string `bson:"_id"`
	Symbol              string `bson:"symbol"`
	shortName           string `bson:"short_name,omitempty"`
	longName            string `bson:"long_name,omitempty"`
	city                string `bson:"city,omitempty"`
	state               string `bson:"state,omitempty"`
	country             string `bson:"country,omitempty"`
	sector              string `bson:"sector,omitempty"`
	industry            string `bson:"industry,omitempty"`
	longBusinessSummary string `bson:"long_business_summary,omitempty"`
}
