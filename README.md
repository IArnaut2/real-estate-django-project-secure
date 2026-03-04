# Real Estate Web App

Web app for advertising apartments for rent via listings.

Any user can:

- View, filter and sort listings
- View all listings of a user

Registered users can:

- Post a listing
- Save listings of other users
- View, edit and delete their own listings
- View, edit and delete their own account

## Models

### Item

| Column | Type         |
| ------ | ------------ |
| id     | BigInt PK    |
| name   | VarChar(255) |

### Terms

| Column         | Type      |
| -------------- | --------- |
| id             | BigInt PK |
| moveInDate     | Date      |
| forStudents    | Boolean   |
| forWorkers     | Boolean   |
| smokingAllowed | Boolean   |
| petsAllowed    | Boolean   |

### Listing

| Column      | Type         |
| ----------- | ------------ |
| id          | BigInt PK    |
| city        | VarChar(255) |
| street      | VarChar(255) |
| storyCount  | Integer      |
| elevator    | Boolean      |
| parking     | Boolean      |
| garage      | Boolean      |
| cctv        | Boolean      |
| intercom    | Boolean      |
| roomCount   | Integer      |
| area        | Integer      |
| story       | Integer      |
| condition   | VarChar(255) |
| heating     | VarChar(255) |
| furnishings | VarChar(255) |
| title       | VarChar(255) |
| description | VarChar(255) |
| price       | Integer      |
| createdAt   | Timestamp    |
| updatedAt   | Timestamp    |
| apartmentId | BigInt FK    |
| termsId     | BigInt FK    |
| posterId    | BigInt FK    |

### ListingItem

| Column    | Type      |
| --------- | --------- |
| listingId | BigInt FK |
| itemId    | BigInt FK |

### User

| Column    | Type         |
| --------- | ------------ |
| id        | BigInt PK    |
| email     | VarChar(255) |
| password  | VarChar(255) |
| phone     | VarChar(255) |
| firstName | VarChar(255) |
| lastName  | VarChar(255) |
| birthDate | Date         |
| createdAt | Timestamp    |
| updatedAt | Timestamp    |

### UserListing

| Column    | Type      |
| --------- | --------- |
| userId    | BigInt FK |
| listingId | BigInt FK |

## Views

### Auth (`AuthController`)

| Done  | Route                | Title        |
| ----- | -------------------- | ------------ |
| **x** | GET `/registracija`  | Registracija |
| **x** | GET `/prijava`       | Prijava      |
| **x** | POST `/registracija` |              |
| **x** | POST `/prijava`      |              |
| **x** | POST `/odjava`       |              |

### Listing (`ListingController`)

| Done  | Route                        | Title                     |
| ----- | ---------------------------- | ------------------------- |
| **x** | GET `/oglasi`                | Svi oglasi                |
| **x** | GET `/oglasi/pretraga`       | Svi oglasi (pretraga)     |
| **x** | GET `/oglasi/postavka`       | Postavka novog oglada     |
| **x** | GET `/oglasi/izmena/{id}`    | Izmena oglasa - `listing` |
| **x** | GET `/oglasi/{id}`           | `listing`                 |
| **x** | POST `/oglasi/postavka`      |                           |
| **x** | POST `/oglasi/izmena/{id}`   |                           |
| **x** | POST `/oglasi/brisanje/{id}` |                           |
| **x** | POST `/oglasi/cuvanje/{id}`  |                           |

### User (`UserController`)

| Done  | Route                        | Title                                  |
| ----- | ---------------------------- | -------------------------------------- |
| **x** | GET `/korisnici/{id}`        | `user`                                 |
| **x** | GET `/korisnici/profil`      | `user`                                 |
| **x** | GET `/korisnici/sacuvani`    | Sačuvani oglasi korisnika `user`       |
| **x** | GET `/korisnici/podesavanje` | Podešavanja korisnika korisnika `user` |
| **x** | POST `/korisnici/izmena`     |                                        |
| **x** | POST `/korisnici/izmena2`    |                                        |
| **x** | POST `/korisnici/brisanje`   |                                        |

## Repositories

### ItemRepository

- [x] `Item[] findAll()`
- [x] `Item[] findByIdIn(data)`

### TermsRepository

- [x] `Terms findOrCreate(data)`
- [x] `void update(long id, data)`
- [x] `void delete(long id)`

### ListingRepository

- [x] `Listing[] findAll()`
- [x] `Listing findById(long id)`
- [x] `void create(Item[] items, Terms terms, data)`
- [x] `void update(long id, Item[] items, data)`
- [x] `void delete(long id)`
- [x] `Listing[] filter(query)`
- [x] `Listing[] findByUser(User user)`
- [x] `Listing[] findSaved(User user)`
- [x] `void save(long id, User user)`

### UserRepository

- [x] `User findById(long id)`
- [x] `User create(data)`
- [x] `void update(long id, data)`
- [x] `void update2(long id, data)`
- [x] `void delete(long id)`
- [x] `User findByEmail(string email)`
- [x] `bool isRegistered(string email)`
- [x] `bool passwordsMatch(string password1, string password2)`

## Security Checklist

- [ ] 1 Parametrized queries
- [ ] 2 Input validation & sanitization
- [ ] 3 CSRF tokens
- [ ] 4 Authentication & authorization
- [ ] 5 Security logging
- [ ] 6 Rate limiting
- [ ] 7 Security headers
- [ ] 8 HTTPS

## Testing

- [ ] SAST
- [ ] DAST
