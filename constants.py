
class Elements:
    # Braintree
    BRAINTREE_TRANSACTION_BUTTON = 'payment-button-TRANSACTION-braintree'
    BRAINTREE_SUBSCRIPTION_BUTTON = 'payment-button-subscription-with-trial-stripe'
    BRAINTREE_TRANSACTION_FORM = 'braintree-sheet__header'
    BRAINTREE_NUMBER_FRAME = 'braintree-hosted-field-number'
    BRAINTREE_NUMBER_FIELD = 'credit-card-number'
    BRAINTREE_EXP_DATE_FRAME = 'braintree-hosted-field-expirationDate'
    BRAINTREE_EXP_DATE_FIELD = 'expiration'

    # Stripe
    STRIPE_TRANSACTION_BUTTON = 'payment-button-TRANSACTION-stripe'
    STRIPE_SUBSCRIPTION_TRIAL_BUTTON = 'payment-button-subscription-with-trial-stripe'
    STRIPE_SUBSCRIPTION_BUTTON = 'payment-button-subscription-stripe'
    STRIPE_NUMBER_FIELD = 'Field-numberInput'
    STRIPE_EXP_DATE_FIELD = 'Field-expiryInput'
    STRIPE_CVC_FIELD = 'Field-cvcInput'

    # Commons
    SCENARIO_SUCCESFUL_PAYMENT = 'scenario-Successful transaction'
    SCENARIO_DECLINED = 'scenario-Declined transaction declined'
    SCENARIO_APPROVED = 'scenario-Declined transaction approved'
    DROPDOWN = 'scenarios-dropdown'
    BACK_TO_CATALOGUE_BUTTON = 'back-to-catalogue-button'
    EXP_DATE_BUTTON = 'copy-expiration-date'
    STATUS_RESPONSE = 'status-message'
    NUMBER_BUTTON = 'copy-card-number'
    CVC_BUTTON = 'copy-cvc'
    CARD_EXPIRED_DATE = '1233'
    PAY_BUTTON = 'submit'
    MESSAGE_ERROR = 'AN ERROR OCCURED'
    MESSAGE_SUCCESFUL_PAYMENT = 'SUCCESFULL PAYMENT'
    MESSAGE_DECLINED = 'DECLINED PAYMENT'
    MESSAGE_APPROVED = 'APPROVED PAYMENT'
