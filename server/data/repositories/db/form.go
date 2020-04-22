package dbRepo

import (
	"fmt"
	"github.com/WISVCH/member-registration/entities"
)

func (repo DBRepo) AddFormEntry(f entities.FormEntity) error {
	repo.logInfo("form", "adding form entry")
	_, err := repo.db.NamedExec("INSERT INTO form_content (" +
		"gender,first_name,last_name,email,phone_number,full_name,street,street_number,postal_code,place,country,letters,netid,yearbook_permission,activity_mailing,career_mailing,education_mailing,machazine,added_to_ldb,freshmen_weekend" +
		") VALUES (" +
		":gender,:first_name,:last_name,:email,:phone_number,:full_name,:street,:street_number,:postal_code,:place,:country,:letters,:netid,:yearbook_permission,:activity_mailing,:career_mailing,:education_mailing,:machazine,:added_to_ldb,:freshmen_weekend" +
		")",
		f)
	fmt.Print(err)
	return err
}


