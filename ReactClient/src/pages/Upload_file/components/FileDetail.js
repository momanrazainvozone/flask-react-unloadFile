export const FileDetail = (props) => {
  return (
    <>
      <h2>File Details:</h2>
      <p>File Name: {props.selectedFile.name}</p>
      <p>File Type: {props.selectedFile.type}</p>
      <p>Last Modified: {props.selectedFile.lastModifiedDate.toDateString()}</p>
    </>
  );
};
