import Alamofire
import SwiftyJSON
import UIKit

class RegistrationViewController: UIViewController {
    
    let URL_USER_REGISTER = Global.getUserURL() + Global.REGISTER_METHOD
    
    @IBOutlet weak var textFieldFirstName: UITextField!
    @IBOutlet weak var textFieldLastName: UITextField!
    @IBOutlet weak var textFieldUsername: UITextField!
    @IBOutlet weak var textFieldPassword: UITextField!
    @IBOutlet weak var textFieldPasswordConfirmation: UITextField!
    
    @IBOutlet weak var textFieldFiscalCode: UITextField!
    @IBOutlet weak var textFieldGender: UITextField!
    @IBOutlet weak var textFieldBirthDate: UITextField!
    @IBOutlet weak var textFieldBirthPlace: UITextField!
    
    @IBAction func registrationToLoginButton(_ sender: Any) {
        self.performSegue(withIdentifier: "registrationToLogin", sender: nil)
    }
    
    @IBOutlet weak var datePicker: UIDatePicker!
    
    @IBAction func registrationButton(_ sender: Any) {
        let parameters: Parameters = [
            "firstname": textFieldFirstName.text!,
            "lastname": textFieldLastName.text!,
            "username": textFieldUsername.text!,
            "password": textFieldPassword.text!,
            "fiscalcode": textFieldFiscalCode.text!,
            "gender": textFieldGender.text!,
            "birthdate": textFieldBirthDate.text!,
            "birthplace": textFieldBirthPlace.text!,
            ]
        
        if (textFieldFirstName.text?.isEmpty ?? true ||
            textFieldLastName.text?.isEmpty ?? true ||
            textFieldUsername.text?.isEmpty ?? true ||
            textFieldPassword.text?.isEmpty ?? true ||
            textFieldPasswordConfirmation.text?.isEmpty ?? true ||
            textFieldFiscalCode.text?.isEmpty ?? true ||
            textFieldGender.text?.isEmpty ?? true ||
            textFieldBirthDate.text?.isEmpty ?? true ||
            textFieldBirthPlace.text?.isEmpty ?? true) {
            let alert = UIAlertController(title: "Attention!", message: "All fields must be completed", preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
            self.present(alert, animated: true)
        }
        else {
            if textFieldPassword.text! == textFieldPasswordConfirmation.text! {
                Alamofire.request(URL_USER_REGISTER, method: .post, parameters: parameters, encoding: JSONEncoding.default)
                    .responseJSON { response in
                        switch response.result {
                        case .success(let value):
                            let json = JSON(value)
                            let code = json["Response"]
                            let reason = json["Reason"].stringValue
                            if code == 1 {
                                let alert = UIAlertController(title: reason, message: "Now you can proceed to login", preferredStyle: .alert)
                                alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: { action in self.performSegue(withIdentifier: "registrationCompleted", sender: nil)}))
                                self.present(alert, animated: true)
                            }
                            else if code == -1 {
                                let alert = UIAlertController(title: reason, message: "Please choose another username", preferredStyle: .alert)
                                alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
                                self.present(alert, animated: true)
                            }
                            else {
                                let alert = UIAlertController(title: "Error!", message: reason, preferredStyle: .alert)
                                alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
                                self.present(alert, animated: true)
                            }
                        case .failure(let error):
                            print(error)
                        }
                }
            }
            else {
                let alert = UIAlertController(title: "Attention!", message: "Passwords do not match", preferredStyle: .alert)
                alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
                self.present(alert, animated: true)
            }
        }
    }
    
    /////////////////////////////////////////////////// DATE KEEPER
    
    @IBAction func dp(_ sender: UITextField) {
        let datePickerView = UIDatePicker()
        datePickerView.datePickerMode = .date
        sender.inputView = datePickerView
        datePickerView.addTarget(self, action: #selector(handleDatePicker(sender:)), for: .valueChanged)
    }
    
    @objc func handleDatePicker(sender: UIDatePicker) {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "dd MMM yyyy"
        textFieldBirthDate.text = dateFormatter.string(from: sender.date)
    }
    
    /////////////////////////////////////////////////// OVERRIDE DEFAULT VIEW FUNCTION
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.hideKeyboardWhenTappedAround()
    }
    
}
