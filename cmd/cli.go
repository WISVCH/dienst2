package cli

import (
	"fmt"
	cfg "github.com/WISVCH/member-registration/config"
	migrations "github.com/WISVCH/member-registration/database"
	"github.com/WISVCH/member-registration/server"
	"github.com/spf13/cobra"
	"os"
)

var (
	verbose            = false
	dbMigrateDirection = ""
	config             = cfg.GetConfig()
	rootCmd            = &cobra.Command{
		Use:   "fantescy",
		Short: "The backend for FantESCy",
		Long:  `The backend application for the FantESCy project`,
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("The FantESCy CLI tool. Run with --help for commands.")
		},
	}
)

func init() {
	// Create root command flags
	rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output (not implemented yet)")

	// Add flags to commands
	serverCmd.Flags().IntVarP(&config.ServerPort, "port", "p", config.ServerPort, "Port for running the Gin server on")
	dbMigrateCmd.Flags().StringVarP(&dbMigrateDirection, "direction", "d", "up|down", "The direction for the database migrations")

	// Required flags
	if err := dbMigrateCmd.MarkFlagRequired("direction"); err != nil {
		panic(err)
	}

	// Add commands	to root command
	rootCmd.AddCommand(serverCmd)
	rootCmd.AddCommand(dbMigrateCmd)
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

var serverCmd = &cobra.Command{
	Use:   "server",
	Short: "Running the backend server application",
	Long:  `The application running the REST API server and doing CRUD operations to the database`,
	Run: func(cmd *cobra.Command, args []string) {
		_ = server.Start(config)
	},
}

var dbMigrateCmd = &cobra.Command{
	Use:   "migrate [up|down]",
	Short: "Database migrator CLI tool",
	Long:  `The CLI tool for managing database migrations`,
	Args:  cobra.OnlyValidArgs,
	Run: func(cmd *cobra.Command, args []string) {
		migrateUp := dbMigrateDirection == "up"
		migrateDown := dbMigrateDirection == "down"
		if !(migrateUp || migrateDown) || (migrateUp && migrateDown) {
			panic("Select migrate up or migrate down")
		}
		if migrateUp {
			if err := migrations.Migrate("up", config); err != nil {
				panic(fmt.Errorf("error running database migrations to latest: %s", err))
			}
			fmt.Println("Database migration up successful")
		}
		if migrateDown {
			if err := migrations.Migrate("down", config); err != nil {
				panic(fmt.Errorf("error running database migrations down: %s", err))
			}
			fmt.Println("Database migration down successful")
		}
	},
}
