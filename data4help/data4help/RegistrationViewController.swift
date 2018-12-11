import Alamofire
import UIKit

extension UIViewController {
    func hideKeyboardWhenTappedAround() {
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(UIViewController.dismissKeyboard))
        view.addGestureRecognizer(tap)
        
    }
    
    @objc func dismissKeyboard() {
        view.endEditing(true)
    }
}

class RegistrationViewController: UIViewController {
    
    let URL_USER_REGISTER = Global.getUserURL() + Global.REGISTER_METHOD
    let GENDERS = ["M", "F"]
    
    @IBOutlet weak var textFieldFirstName: UITextField!
    @IBOutlet weak var textFieldLastName: UITextField!
    @IBOutlet weak var textFieldUsername: UITextField!
    @IBOutlet weak var textFieldPassword: UITextField!
    
    @IBOutlet weak var textFieldBirthPlace: UITextField!
    @IBOutlet weak var textFieldBirthDate: UITextField!
    
    @IBOutlet weak var textFieldGender: UITextField!
    
    @IBOutlet weak var textFieldFiscalCode: UITextField!
    
    @IBOutlet weak var labelMessage: UILabel!
    
    @IBAction func buttonRegister(_ sender: UIButton) {
        let parameters : Parameters=[
            "firstname":textFieldFirstName.text!,
            "lastname":textFieldLastName.text!,
            "username":textFieldUsername.text!,
            "password":textFieldPassword.text!
        ]
        Alamofire.request(URL_USER_REGISTER, method: .post, parameters: parameters, encoding: JSONEncoding.default)
            .responseJSON {
                response in
                if let status = response.result.value {
                    let JSON = status as! NSDictionary;
                    let appo = JSON["Response"]!;
                    print(appo)
                }
        }
    }

    
    override func viewDidLoad() {
        super.viewDidLoad()
//        genderPicker.isHidden = true
        self.hideKeyboardWhenTappedAround()
    }
    
}
