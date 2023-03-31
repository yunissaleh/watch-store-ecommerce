# watch-store-ecommerce
This is an auction web application built using Django that allows users to create auction listings, bid on listings, add listings to a watchlist, and comment on listings. The application has the following features:

# Models
The application has the following models:

- User: for user authentication
- Listing: for auction listings
- Bid: for bids on auction listings
- Comment: for comments on auction listings

# Create Listing
Users can create a new auction listing by visiting the create listing page. They can specify a title, description, starting bid, and optionally provide an image URL and category for the listing.

# Active Listings Page
The default route of the web application displays all active auction listings. For each listing, the title, description, current price, and photo (if one exists) are displayed.

# Listing Page
Clicking on a listing takes users to a page specific to that listing. On that page, users can view all details about the listing, including the current price. If the user is signed in, they can add the item to their watchlist, bid on the item, or close the auction if they are the listing owner. If a user has won a closed auction, the page displays a message indicating that they have won. Users who are signed in can also add comments to the listing page, and all comments are displayed.

# Watchlist
Users who are signed in can visit their watchlist page, which displays all the listings that they have added to their watchlist. Clicking on any of those listings takes the user to that listing's page.

# Categories
Users can visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all active listings in that category.
