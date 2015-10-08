from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import *
import simplejson as json
import codecs
from boto.mturk.connection import MTurkConnection


class Command(BaseCommand):
    help = "lists mturk assignments"

    def add_arguments(self, parser):
        pass

    def get_all_reviewable_hits(self,mtc):
        page_size = 50
        hits = mtc.get_reviewable_hits(page_size=page_size)
        print "Total results to fetch %s " % hits.TotalNumResults
        print "Request hits page %i" % 1
        total_pages = float(hits.TotalNumResults)/page_size
        int_total= int(total_pages)
        if(total_pages-int_total>0):
            total_pages = int_total+1
        else:
            total_pages = int_total
        pn = 1
        while pn < total_pages:
            pn = pn + 1
            print "Request hits page %i" % pn
            temp_hits = mtc.get_reviewable_hits(
                page_size=page_size,
                page_number=pn)
            hits.extend(temp_hits)
        return hits


    def handle(self, *args, **options):
        """handle the command."""

        mtc = MTurkConnection(debug=1)
        hits = self.get_all_reviewable_hits(mtc)

        for hit in hits:
            assignments = mtc.get_assignments(hit.HITId)
            for assignment in assignments:
                print "Survey Code for Worker %s: %s" % (
                    assignment.WorkerId,
                    assignment.answers[0][0].fields[0])


