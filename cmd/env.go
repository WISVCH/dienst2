package cli

import (
	"fmt"
	cfg "github.com/WISVCH/member-registration/config"
	"github.com/spf13/viper"
)

func getConfig() cfg.Config {
	config, err := loadConfig()
	if err != nil { // Handle errors reading the config file
		panic(fmt.Errorf("Fatal error config file: %s \n", err))
	}
	fmt.Println("Config file successfully loaded")
	return config
}

func loadConfig() (cfg.Config, error) {
	v := viper.New()
	v.SetConfigType("toml")
	v.SetConfigFile(".env")
	err := v.ReadInConfig() // Find and read the config file
	if err != nil {
		return cfg.Config{}, err
	}

	var config cfg.Config
	err = v.Unmarshal(&config)
	if err != nil {
		return cfg.Config{}, err
	}

	isValidConfig := validateConfig(config)
	if !isValidConfig {
		err = fmt.Errorf("config validation failed with config %#v", config)
	}
	return config, err
}

func validateConfig(config cfg.Config) bool {
	if config.DatabaseHost == "" || config.DatabasePort == 0 || config.DatabaseName == "" || config.DatabaseUser == "" || config.JWTSecret == "" {
		return false
	}
	return true
}
