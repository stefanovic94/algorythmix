package entities

type Asset struct {
	ID                  string `bson:"_id"`
	Symbol              string `bson:"symbol"`
	ShortName           string `bson:"short_name"`
	LongName            string `bson:"long_name"`
	City                string `bson:"city"`
	State               string `bson:"state"`
	Country             string `bson:"country"`
	Sector              string `bson:"sector"`
	Industry            string `bson:"industry"`
	LongBusinessSummary string `bson:"long_business_summary"`
}
