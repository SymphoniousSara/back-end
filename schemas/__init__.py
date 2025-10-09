from schemas.birthdays import *
from schemas.contributions import *
from schemas.users import *
from schemas.gifts import *

BirthdayWithDetailsSchema.model_rebuild()
BirthdayWithContributionsSchema.model_rebuild()
ContributionWithRelationsSchema.model_rebuild()
ContributionWithContributorSchema.model_rebuild()
