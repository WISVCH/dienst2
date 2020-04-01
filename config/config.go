package config

import "fmt"

type Config struct {
	IsDevMode              bool   `mapstructure:"development"`
	ServerPort             int    `mapstructure:"server_port"`
	DatabaseHost           string `mapstructure:"db_host"`
	DatabasePort           int    `mapstructure:"db_port"`
	DatabaseName           string `mapstructure:"db_name"`
	DatabaseUser           string `mapstructure:"db_user"`
	DatabasePass           string `mapstructure:"db_pass"`
}

func (c Config) DatabaseConnectionString() string {
	connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s",
		c.DatabaseHost, c.DatabasePort, c.DatabaseUser, c.DatabasePass, c.DatabaseName)
	return connStr
}
