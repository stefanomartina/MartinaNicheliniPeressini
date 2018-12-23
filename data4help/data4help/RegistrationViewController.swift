import Alamofire
import SwiftyJSON
import UIKit

class RegistrationViewController: UIViewController,
            UIPickerViewDelegate, UIPickerViewDataSource, UITextFieldDelegate {
    
    let URL_USER_REGISTER = Global.getUserURL() + Global.REGISTER_METHOD
    let genders = ["M", "F"]
    
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
    
    // GENDER PICKER FUNCTIONS
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return genders.count
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return genders[row]
    }
    
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        textFieldGender.text = genders[row]
    } // END GENDER PICKER FUNCTIONS
    
    // DATE PICKER FUNCTIONS
    @objc func datePickerValueChanged(sender: UIDatePicker) {
        let formatter = DateFormatter()
        formatter.dateStyle = DateFormatter.Style.medium
        formatter.timeStyle = DateFormatter.Style.none
        formatter.dateFormat = "yyyy-MM-dd"
        textFieldBirthDate.text = formatter.string(from: sender.date)
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        view.endEditing(true)
    } // END DATE PICKER FUNCTIONS
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // GENDER PICKER DECLARATION
        let genderPicker = UIPickerView()
        textFieldGender.inputView = genderPicker
        genderPicker.delegate = self
        
        // DATE PICKER DECLARATION
        let datePicker = UIDatePicker()
        datePicker.datePickerMode = UIDatePicker.Mode.date
        datePicker.addTarget(self, action: #selector(RegistrationViewController.datePickerValueChanged(sender:)),
                             for: UIControl.Event.valueChanged)
        textFieldBirthDate.inputView = datePicker
        textFieldBirthDate.delegate = self
        
        self.hideKeyboardWhenTappedAround() // to resign view at a tap out
        
        self.textFieldFirstName.delegate = self
        self.textFieldFirstName.delegate = self
        self.textFieldLastName.delegate = self
        self.textFieldUsername.delegate = self
        self.textFieldPassword.delegate = self
        self.textFieldPasswordConfirmation.delegate = self
        self.textFieldFiscalCode.delegate = self
        self.textFieldGender.delegate = self
        self.textFieldBirthDate.delegate = self
        self.textFieldBirthPlace.delegate = self
        
        textFieldFirstName.tag = 0
        textFieldLastName.tag = 1
        textFieldUsername.tag = 2
        textFieldPassword.tag = 3
        textFieldPasswordConfirmation.tag = 4
        textFieldFiscalCode.tag = 5
        textFieldGender.tag = 6
        textFieldBirthDate.tag = 7
        textFieldBirthPlace.tag = 8
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool
    {
        // Try to find next responder
        if let nextField = textField.superview?.viewWithTag(textField.tag + 1) as? UITextField {
            nextField.becomeFirstResponder()
        } else {
            // Not found, so remove keyboard.
            textField.resignFirstResponder()
        }
        // Do not add a line break
        return false
    }
    
    ////////////////////////////////////////// Picker toolbar
    
    func pickUp(_ textField : UITextField){
        
        // ToolBar
        let toolBar = UIToolbar()
        toolBar.barStyle = .default
        toolBar.isTranslucent = true
        toolBar.tintColor = UIColor(red: 92/255, green: 216/255, blue: 255/255, alpha: 1)
        toolBar.sizeToFit()
        
        //Adding Button ToolBar
        let doneButton = UIBarButtonItem(title: "Done", style: .plain, target: self, action: #selector(self.doneClick))
        
        toolBar.setItems([doneButton], animated: false)
        toolBar.isUserInteractionEnabled = true
        textField.inputAccessoryView = toolBar
    }
    
    func textFieldDidBeginEditing(_ textField: UITextField) {
        self.pickUp(textField)
    }
    
    @objc func doneClick() {
        if textFieldGender.isFirstResponder{ textFieldGender.resignFirstResponder()}
        else {textFieldBirthDate.resignFirstResponder()}
    }
}
