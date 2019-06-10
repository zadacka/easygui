from boxes.multi_fillable_box import multenterbox


def multienterbox_demo():
    user_values = multenterbox(msg="Enter your personal information",
                               title="Credit Card Application",
                               fields=["Name", "Street Address", "City", "State", "ZipCode"],
                               values=[])
    print("Reply was: {}".format(user_values))


if __name__ == '__main__':
    multienterbox_demo()
