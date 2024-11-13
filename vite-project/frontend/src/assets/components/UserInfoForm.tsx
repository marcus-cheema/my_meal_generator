import '../../App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';

import { getBmrCalculation } from '../../services/apiServices';
import React, { useState } from 'react';

export interface UserFormProps {
    sex: string;
    age: string;
    weight: string;
    height: string;
    activityLevel: string;
    bmr: string;
}

function UserInfoForm() {
    let [formData, setFormData] = useState<UserFormProps>({ //default
        sex: '',
        age: '',
        weight: '',
        height: '',
        activityLevel: '',
        bmr:'(Not Calculated)'
    });

    let handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        let { name, value } = e.target; 
        setFormData((prevFormData) => ({
        ...prevFormData,
        [name]: value,
        }));
    };

    let handleSubmit = async(e: React.FormEvent) => {
        e.preventDefault();
        try {
            let response = await getBmrCalculation(formData);
            let userBmr = 2000;
            if (response != null) {
                userBmr = response.data.response;
            }
            console.log("Here is the BMR", userBmr);
            setFormData(prevFormData => ({
                ...prevFormData,
                bmr: userBmr.toString()
            }));
        } catch(error) {
            console.error("could not calculate BMR", error);
        }    
    }   
    
    return(
        <>
            <button type="button" className="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#bmrModal">Calculate BMR</button>
            <div className="modal fade" id="bmrModal" tabIndex={-1} aria-labelledby='bmrModalLabel' aria-hidden="true">
                <div className="modal-dialog">
                    <div className='modal-content'>
                        <div className='modal-header'>
                            <h5 className="modal-title" id="bmrModalLabel">Your BMR (Calories/Day): {formData.bmr}</h5>
                            <button
                                type="button"
                                className="btn-close"
                                data-bs-dismiss="modal"
                                aria-label="Close"
                            ></button>    
                        </div>
                        <div className="modal-body">
                            <form onSubmit={handleSubmit}>
                                <div className="mb-3">
                                    <label htmlFor="sex" className="form-label">Sex</label>
                                    <select
                                        className="form-select"
                                        id="sex"
                                        name="sex"
                                        value={formData.sex}
                                        onChange={handleInputChange}
                                    >
                                        <option value="">Select Sex</option>
                                        <option value="male">Male</option>
                                        <option value="female">Female</option>
                                    </select>
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="age" className="form-label">Age (years)</label>
                                    <input
                                        type="number"
                                        className="form-control"
                                        id="age"
                                        name="age"
                                        value={formData.age}
                                        onChange={handleInputChange}
                                        placeholder="Enter your age"
                                    />
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="weight" className="form-label">Weight (lbs)</label>
                                    <input
                                        type="number"
                                        className="form-control"
                                        id="weight"
                                        name="weight"
                                        value={formData.weight}
                                        onChange={handleInputChange}
                                        placeholder="Enter your weight"
                                    />
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="height" className="form-label">Height (inches) </label>
                                    <input
                                        type="number"
                                        className="form-control"
                                        id="height"
                                        name="height"
                                        value={formData.height}
                                        onChange={handleInputChange}
                                        placeholder="Enter your height"
                                    />
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="activityLevel" className="form-label">Activity Level</label>
                                    <select
                                        className="form-select"
                                        id="activityLevel"
                                        name="activityLevel"
                                        value={formData.activityLevel}
                                        onChange={handleInputChange}
                                    >
                                        <option value="">Select activity level</option>
                                        <option value="sedentary">Sedentary (little or no exercise)</option>
                                        <option value="light">Lightly active (1-3 days/week)</option>
                                        <option value="moderate">Moderately active (3-5 days/week)</option>
                                        <option value="very">Very active (6-7 days/week)</option>
                                        <option value="extra">Extra active (very active + physical job)</option>
                                    </select>
                                </div>
                                
                                <div className="modal-footer">
                                    <button 
                                        type="button" 
                                        className="btn btn-secondary" 
                                        data-bs-dismiss="modal"
                                    >
                                    Close
                                    </button>
                                    <button type="submit" className="btn btn-primary">Calculate</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </> 
    )
}

export default UserInfoForm