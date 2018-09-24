# INTRODUCTION TO PLUG TRANSFORMS

## OBJECTIVES

- Create a Transform that adds free money to a specific Users balance.
- Create a Transform that can transfer money between two Users
- Rewrite your code to use the Plug `api_client`.

### SETUP

1. Clone down the `plug-intro` repository into your workspace folder.

1. Navigate into the `plug-intro` repository and enter the pip shell using the `pipenv shell` command.
**Note: You must have pip, pipenv and python (v 3.6 or higher).**

1. Run `pipenv install ../plug/libs/plug-0.0.20.tar.gz`, with the correct path to your local copy of the plug repository.

1. Do the same for `pipenv install ../plug/libs/plug-api-1.6.1.tar.gz`.

1. Run `pipenv install -e .` to make sure everything you need is installed.

1. If your installation went according to plan, you should be able to run `plug-dev create-network -n1 node.yaml -d ./nodes` which will automatically create a `/nodes` directory with a `node_0` directory inside it.

1. Navigate into the `node_0` directory and enter the command `plug run`. Your terminal should now burst to life and display some delightful ascii art.

1. Head over to http://localhost:8181/_swagger and make sure the server has spun up properly.

```

       _
 _ __ | |_   _  __ _
| '_ \| | | | |/ _` |
| |_) | | |_| | (_| |
| .__/|_|\__,_|\__, |
|_|            |___/   


```

1. You can run the tests with `python setup.py test`

### OBJECTIVE: CREATE A BALANCE TRANSFER TRANSFORM

We're going to write a new BalanceTransfer class that extends Transform. This transform will be able to transfer money from the balance of one user to another.

#### Step One: Generating another User.

There must be multiple Users within the blockchain to allow the transfer of money back and forth.
In a new terminal window, run `python client create_user` from the root of your project. This should add a new User into the blockchain, and print out their pertinent information into your console.

Remember to keep a record of the new User key. You will need these later! We'll use them to transform and query the blockchain.

#### Step Two: Writing the BalanceTransfer transform.

It's time to head over to `transform.py`. Define a new `BalanceTransfer` class that extends Transform, and fill in the required methods. If you get stuck, remember to _consult the Plug documentation on writing Transforms_.

The real logic takes place in the `verify()` and `apply()` methods. In `verify()`, you need to make sure that the sender actually _has_ a sufficient balance to cover the transfer, and then in `apply()` you will alter the user balances.

#### Step Three: Add the BalanceTransfer class to your components array.

Back in `__init.py__` you must _add your new transform to the component list_:

```
components = [
# Include your plugin's
...
free_money.transform.BalanceTransfer,
]
```

#### Step Four: Transfer some Balance!

From the root of your project, run the `python client transaction` command and follow the prompts. If everything went according to plan, you should now be able to run `python client balance_query` on your users and see the balance has transferred successfully.

### OBJECTIVE: CREATE A FREE MONEY TRANSFORM

Now we're going to create a new FreeMoney class that extends Transform. This transform will allow us to give some free money to a specific user.

#### Step One: Checking their balance.

All users are created equal in this blockchain. When a new User is added, they receive a starting balance of 100. Try running `python client balance_query` from your terminal and enter the `address` from earlier when prompted. This should print the User balance in your log.

#### Step Two: Writing the FreeMoney transform.

Now it's time to write the FreeMoney class in `transform.py`. This class extends Transform, and has several required methods to work correctly. *Check out the plug documentation for a reference on writing Transforms.*

This is actually a very simple transform. Essentially there are only two things you need to check for. In the `verify()` method, you need to _verify_ that the amount you are trying to add to the User's balance is _greater than 0._

Then, most important of all, in the `apply()` method, the actual transformation needs to take place. This will require referencing a `balances` object from the `state_slice[]`, and using your `BalanceModel.fqdn` as the indexer. Once you have that `balances[]` reference, you can use the address of the the `self.receiver` as an index and increment their balance by the desired amount.

You still need to flesh out the other required methods too, but they are fairly standard. Use the BalanceTransfer transform as a reference.

#### Step Three: Add the FreeMoney transform to your components array.

Over in `__init.py__` _add your new FreeMoney transform to this list_:

```
  components = [
      # Include your plugins
      ...
      free_money.transform.BalanceTransfer,
      free_money.transform.FreeMoney,
  ]
```

#### Step Four: Writing the FreeMoney client.

Head over to `free_money.py`. The first step here is going to be getting a reference to your desired user object. Luckily, because this script is going to be triggered by user input on the command line, we have the `address_input` and `amount` arguments to pass into our transform.

#### Step Five: Give some free money.

Try running `python client free_money` from your root directory; you should receive a OK status code back. To double check that our User did indeed receive their free money, run `python client balance_query` again with the same `address` and their balance should have increased.

#### Congratulations!

You have successfully written a Transform that gives unlimited, free money to a specific User in the blockchain. Please note; _it is unlikely that your employer will ever request that this specific feature be implemented for financial reasons._

#### Step Six: Integrate the Plug api_client.

The Plug API Client is a library for sending requests to Plug nodes via the HTTP API. It provides several classes to make interacting with the nodes faster, and helps with local storage of signing keys, addresses and nonces.
So naturally, in classic programmer style, we're going to destroy most of the code you just wrote and start again.

If you haven't already, head over to this page on the [Plug API Client](https://github.com/dev-academy-programme/plug-resources/blob/free-money-overview/segments/plug/api-client.md) and follow the setup instructions.

The real trick here is integrating `broadcast_transform` into your client code. Once you have done that, all of your scripts can be extremely slim and elegant. If you get stuck at any point, don't forget to head over to [the free money solution walkthrough for help.](https://github.com/dev-academy-programme/plug-resources/blob/free-money-overview/segments/challenges/free-money-solution.md)

#### Where to from here?

- Write another Transform that can compare the balances of two Users and return the difference.
