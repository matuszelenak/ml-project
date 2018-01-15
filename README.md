# ml-project
Project for a FMFI Machine Learning course

Usage:
If you just want to train the model on existing data, run

./train_model.py --train --n prefix_path_to_dataset

For example, to train model with 5 neural networks on the existing data in repository and save both the models and the testing results, run

./train_model.py --train --dataset ./datasets/dataset_v2_ --eval --n 5 --savem --saver

If you want to run XVM prediction on the same test set the neural network model used, run
./XVM.py path_to_results
for example 
./XVM.py ./results/2018011517_25_47/

If you want to process raw JSON files produced by WoT Replay Analyzer, run
./process_raw_json.py
It draws JSONs from replay_jsons folder and outputs processed files into replays_simple.

If you want to update the tank and map statistics, before creating dataset, run
./scrape_vbaddict.py

If you want to create a dataset out of the files in replays_simple, run
./construct_dataset

To visualize the results run
./visualize_data.py path_to_results
so for example
./visualize_data.py ./results/2018011517_25_47/
