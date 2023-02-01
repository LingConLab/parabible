## Massively Parallel Text Corpus

Available Data
--------------

The massively parallel text corpus currently consists of three projects:

- **Parallel Bible Corpus** (subdirectory /bibles)
- **Universal Declarations of Human Rights** (subdirectory /udhr)
- **Watchtower Corpus** (subdirectory /watchtower)

The bible corpus is in pretty good shape, but the other corpora are in need of more error checking. Please be careful when using those corpora.

File names
----------

The file names used are defining each text as a **doculect** ([Cysouw & Good 2013](http://hdl.handle.net/10125/4606)).

The file names follow the IETF standard [BCP 47](https://tools.ietf.org/html/bcp47) for language identification, consisting of tags delimited by dashes. The first tag is the closest available [ISO 639-3 code](http://www.sil.org/iso639%2D3). Note that this is often a rather rough approximation of the language used in the specific file! Then comes an `x` to delimit private-use tags, followed by a corpus tag, currently either `bible`, `udhr`, or `watchtower`. Additionally, various ad-hoc tags are used to make each file unique, using either dialect names or translation names.

TO DO: as proposed in BCP 47, script and region tags should be added before the private-use delimiter `-x-`.

Data Format
-----------

- All files have metadata on top in a basic `key:value` format. 
- Hashes at the start of a line indicate lines to be excluded to obtain the core data. 
- The core data always consist of two columns, separated by a tab. 
	* The first column is an identifier of the parallelism.
	* The second column contains the actual data.
- Lines with an identifier in the first column, but with an empty second column indicate that the content of this parallel chunk is expected to be part of the last full data line above the empty second column.
- Absent identifiers indicate that this parallel chunk is to our knowledge not available in the current version.

About data sharing
------------------

The texts collected here are in a private repository because the licenses for many texts are not open. So please **do not spread these files freely around**. If you know of somebody interested in participating advancing the status of these corpus, please refer them to the maintainers.

This git repository allows for direct push of changes, so any minor changes can just be directly pushed to master. However, I propose that **if you want to suggest major changes, then you should use a pull request** so we can discuss those changes separately.

The basic texts are in the subdirectory `/corpus`.These texts should only changed when really necessary, i.e. when there are errors in the texts. **Any annotations or other additional information should be stored in some kind of stand-off annotations in separate directories.**

Citation
--------

We try to be as precise as possible adding sources to all data in this repository. Please cite those source accordingly when you use the data. Further, as an acknowledgement of the preparation of this repository, please also cite:

Mayer, Thomas & Michael Cysouw. 2014. Creating a Massively Parallel Bible Corpus. Proceedings of the International Conference on Language Resources and Evaluation (LREC), Reykjavik, 3158-3163. [paper](http://www.lrec-conf.org/proceedings/lrec2014/pdf/220_Paper.pdf)

Maintainers
-----------

* __Michael Cysouw__  
	<cysouw@uni-marburg.de>  
	<http://cysouw.de/home>
	
* __Thomas Mayer__  
	<thommy.mayer@gmail.com>  
	<http://th-mayer.de>

* __Frank Nagel__  
	<frank.nagel@uni-marburg.de>
