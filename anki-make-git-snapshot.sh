#!/bin/sh

# Usage: sh anki-make-git-snapshot.sh [LIBANKICOMMIT] [ANKIQTCOMMIT] [DATE]
#
# to make a snapshot of the given tag/branch.  Defaults to HEAD.

set +x

if [ -z $3 ]; then
  DATE=`date +%Y%m%d`
else
  DATE=$3
fi

DIRNAME="anki-$DATE"

echo DIRNAME $DIRNAME
echo LIBANKIHEAD ${1:-HEAD}
echo ANKIQTHEAD ${2:-HEAD}

rm -rf $DIRNAME

git clone git://github.com/dae/ankiqt.git $DIRNAME
git clone git://github.com/dae/libanki.git $DIRNAME/libanki

pushd $DIRNAME 
git checkout $ANKIQTHEAD
pushd libanki
git checkout $LIBANKIHEAD
popd
popd

ln -s $DIRNAME ankiqt
ln -s $DIRNAME/libanki libanki
bzr clone lp:anki
pushd anki
./update-mos.sh
popd
rm ankiqt
rm libanki
rm -rf anki

rm -rf $DIRNAME/.git $DIRNAME/libanki/.git
rm -rf $DIRNAME/libanki/tests/importing/supermemo*

tar czf $DIRNAME.tgz $DIRNAME

rm -rf $DIRNAME

