package entities

type Asset struct {
	ID                  string `bson:"_id"`
	Symbol              string `bson:"symbol"`
	ShortName           string `bson:"short_name,omitempty"`
	LongName            string `bson:"long_name,omitempty"`
	City                string `bson:"city,omitempty"`
	State               string `bson:"state,omitempty"`
	Country             string `bson:"country,omitempty"`
	Sector              string `bson:"sector,omitempty"`
	Industry            string `bson:"industry,omitempty"`
	LongBusinessSummary string `bson:"long_business_summary,omitempty"`
}
