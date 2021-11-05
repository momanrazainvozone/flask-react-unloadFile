import { useState } from "react";
import axios from "axios";
import CircularProgress from "@mui/material/CircularProgress";
import { FileUplaoded } from "./components/FileUplaoded";
import { FileDetail } from "./components/FileDetail";
import "./uploadFile.css";
export const UploadFile = () => {
  const [selectedFile, setselectedFile] = useState();
  const [isFileUplaoded, setisFileUplaoded] = useState(false);
  const [uplaodingFile, setuplaodingFile] = useState(false);
  //===================={FUNCTIONS}==================//
  const onFileChange = (event) => {
    setselectedFile(event.target.files[0]);
  };
  const uploadFile = async () => {
    setuplaodingFile(true);
    const form_data = new FormData();
    form_data.append("file", selectedFile);

    const reqObj = {
      method: "POST",
      url: "http://18.118.116.85:8000/upload",
      data: form_data,
    };
    const results = await axios(reqObj);
    if (results.status === 200) {
      setisFileUplaoded(true);
      setselectedFile(null);
      setuplaodingFile(false);
    }
  };
  //========================{RENDRING COMPONENTS}===================//
  if (uplaodingFile) {
    return <CircularProgress className="circularbar" />;
  }
  if (selectedFile) {
    return (
      <div>
        <FileUplaoded isFileUplaoded={isFileUplaoded} />
        <h1 className="textCenter">Send File to flask</h1>
        <FileDetail selectedFile={selectedFile} />
        <button onClick={() => uploadFile()}>Send!</button>
      </div>
    );
  }
  return (
    <div>
      <FileUplaoded isFileUplaoded={isFileUplaoded} />
      <h1 className="textCenter">Send File to flask</h1>
      <br />
      <h4>Choose before Pressing the Upload button</h4>
      <input type="file" onChange={(event) => onFileChange(event)} />
    </div>
  );
};
export default UploadFile;
