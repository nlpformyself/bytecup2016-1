import pandas as pa
training_data_formatted = pa.read_csv("./bytecup2016data/invited_info_train.txt", sep = "\t", names=["qid","uid","label"] )
pred_df= pa.DataFrame({'label': y_pred_train_str})
result = pa.concat([training_data_formatted.ix[:,0:2], pred_df], axis=1)
result.to_csv('CollFiltering_train_1.csv', index=False, columns=["qid","uid","label"])
