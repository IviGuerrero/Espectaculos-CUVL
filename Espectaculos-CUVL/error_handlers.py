from flask import render_template

def handle_db_error(error):
    return render_template ('500.html'),500    

def handle_404_error(error):
    return render_template ('404.html'),404
    