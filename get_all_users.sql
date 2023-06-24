SELECT TOP (1000) U.user_id,
    U.name AS user_name,
    U.username,
    U.email,
    U.phone,
    U.website,
    A.street,
    A.suite,
    A.city,
    A.zipcode,
    G.lat,
    G.lng,
    C.name AS company_name,
    C.catchphrase,
    C.bs
FROM [User] U
    INNER JOIN Address A ON U.address_id = A.address_id
    INNER JOIN Geo G ON A.geo_id = G.geo_id
    INNER JOIN Company C ON U.company_id = C.company_id;