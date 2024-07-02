from ext import app






if __name__ == "__main__":
    from routes import home, register, login, about, profile, stadium, product, create_product, edit_product, delete_product, create_club, edit_club,add_to_cart,cart,remove_from_cart,contact,thankyou,order
    app.run(debug=True)
