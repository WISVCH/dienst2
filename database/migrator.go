package migrations

import (
	"database/sql"
	"fmt"
	"github.com/golang-migrate/migrate/v4"
	"github.com/golang-migrate/migrate/v4/database/postgres"
	_ "github.com/golang-migrate/migrate/v4/source/file"
	_ "github.com/lib/pq"
	"os"
)

func Migrate(direction string, config config.Config) error {
	// Direction check
	if direction != "up" && direction != "down" {
		return fmt.Errorf("Migration direction should be 'up' or 'down'")
	}

	// Database connection instance
	psqlInfo := config.DatabaseConnectionString()
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		return err
	}
	defer db.Close()

	// Generating migration instance
	driver, err := postgres.WithInstance(db, &postgres.Config{})
	if err != nil {
		return err
	}
	workingDir, err := os.Getwd()
	if err != nil {
		return err
	}
	sourceURL := "file://" + workingDir + "/database/migrations" // TODO: Make less error prone
	migrator, err := migrate.NewWithDatabaseInstance(sourceURL, "postgres", driver)
	if err != nil {
		return err
	}

	// Run migrator
	if direction == "up" {
		return migrator.Up()
	}
	if direction == "down" {
		return migrator.Down()
	}
	return fmt.Errorf("no database migrations ran")
}
