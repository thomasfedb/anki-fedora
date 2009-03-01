#!/bin/sh

VERSION=$1

tar -xzvf anki-$VERSION.tgz
rm -rf anki-$VERSION/libanki/samples

tar -czvf anki-$VERSION-nosamples.tgz anki-$VERSION

